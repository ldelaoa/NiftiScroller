import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import SimpleITK as sitk
import tkinter as tk
from tkinter import filedialog, messagebox

class SliceViewer:
    def __init__(self, ct_data, seg_data, dl_data):
        self.ct_data = ct_data
        self.seg_data = seg_data
        self.dl_data = dl_data

        self.view = 'axial'  # 'axial', 'coronal', or 'sagittal'
        self.slice_index = ct_data.shape[0] // 2

        self.GTshow_contour = True
        self.DLshow_contour = True
        self.secondImage_cmap = 'rainbow'

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)


        self.update_display()

    def get_slice(self, data):
        if self.view == 'axial':
            return data[self.slice_index, :, :]
        elif self.view == 'coronal':
            return data[:, self.slice_index, :]
        elif self.view == 'sagittal':
            return data[:, :, self.slice_index]
            

    def update_display(self):
        self.ax.clear()
        ct_slice = self.get_slice(self.ct_data)
        self.ax.imshow(ct_slice, cmap='gray')

        if self.GTshow_contour:
            seg_slice = self.get_slice(self.seg_data)
            contours = measure.find_contours(seg_slice, 0.5)
            for contour in contours:
                self.ax.plot(contour[:, 1], contour[:, 0], linewidth=1.5, color='red')

        if self.DLshow_contour:
            dl_slice = self.get_slice(self.dl_data)
            masked_dl = np.ma.masked_where(dl_slice == 0, dl_slice)
            self.ax.imshow(masked_dl, cmap=self.secondImage_cmap, alpha=0.5)


        self.ax.set_title(f"{self.view.capitalize()} Slice {self.slice_index} | GT [g]: {'On' if self.GTshow_contour else 'Off'} | DL [d]: {'On' if self.DLshow_contour else 'Off'} | Colormap [m]: {'P map' if self.secondImage_cmap == 'rainbow' else 'PET'}")

        if self.view != 'axial':
            self.ax.invert_yaxis()
        self.ax.axis('off')
        plt.draw()

    def on_scroll(self, event):
        max_index = {
            'axial': self.ct_data.shape[0],
            'coronal': self.ct_data.shape[1],
            'sagittal': self.ct_data.shape[2]
        }[self.view]

        if event.button == 'up':
            self.slice_index = min(self.slice_index + 1, max_index - 1)
        elif event.button == 'down':
            self.slice_index = max(self.slice_index - 1, 0)
        self.update_display()

    def on_click(self, event):
        self.GTshow_contour = not self.GTshow_contour
        self.update_display()

    def on_key(self, event):
        if event.key == 'up':
            self.on_scroll(type('event', (object,), {'button': 'up'}))
        elif event.key == 'down':
            self.on_scroll(type('event', (object,), {'button': 'down'}))
        elif event.key == 'g':
            self.GTshow_contour = not self.GTshow_contour
        elif event.key == 'd':
            self.DLshow_contour = not self.DLshow_contour
        elif event.key == 'v':
            self.toggle_view()
        elif event.key == 'm':
            self.secondImage_cmap = 'hot' if self.secondImage_cmap == 'rainbow' else 'rainbow'

        self.update_display()

    def toggle_view(self):
        views = ['axial', 'coronal', 'sagittal']
        current_index = views.index(self.view)
        self.view = views[(current_index + 1) % len(views)]
        self.slice_index = {
            'axial': self.ct_data.shape[0] // 2,
            'coronal': self.ct_data.shape[1] // 2,
            'sagittal': self.ct_data.shape[2] // 2
        }[self.view]


def normalize_image(image, vmin, vmax):
    return (image - vmin) / (vmax - vmin)

def main():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("SliceViewer Instructions","🧠 SliceViewer Controls:\n\n""- Scroll or ↑/↓: Navigate slices\n"
                        "- g: Toggle Ground Truth contours\n"
                        "- d: Toggle DL segmentation overlay\n"
                        "- v: Switch view (Axial / Coronal / Sagittal)\n"
                        "- m: Switch colormap (Rainbow (Probability Map) / Hot (PET))\n"
                        "- Mouse Click: Toggle GT contours\n\n"
                        "You will now be asked to select 3 image files:\n"
                        "1. CT scan\n"
                        "2. Ground Truth segmentation\n"
                        "3. DL segmentation\n\n")
    
    #init_dir = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/Sharing/RobinWi/PatientsToReview/"

    #ct_path = filedialog.askopenfilename(title="Select CT Data", initialdir=init_dir,filetypes=[("All files", "*.*")])
    #seg_path = filedialog.askopenfilename(title="Select Ground Truth Segmentation", initialdir=init_dir,filetypes=[("All files", "*.*")])
    #dl_path = filedialog.askopenfilename(title="Select DL Segmentation", initialdir=init_dir,filetypes=[("All files", "*.*")])
    ct_path = filedialog.askopenfilename(title="Select CT Data", filetypes=[("All files", "*.*")])
    seg_path = filedialog.askopenfilename(title="Select Ground Truth Segmentation", filetypes=[("All files", "*.*")])
    dl_path = filedialog.askopenfilename(title="Select DL Segmentation", filetypes=[("All files", "*.*")])

    if not ct_path or not seg_path or not dl_path:
        messagebox.showerror("Error", "All three files must be selected.")
        return

    ct_data = sitk.GetArrayFromImage(sitk.ReadImage(ct_path))
    seg_data = sitk.GetArrayFromImage(sitk.ReadImage(seg_path))
    dl_data = sitk.GetArrayFromImage(sitk.ReadImage(dl_path))

    if ct_data.shape != seg_data.shape or ct_data.shape != dl_data.shape:
        messagebox.showerror("Error", "All input arrays must have the same shape.")
        return

    viewer = SliceViewer(ct_data, seg_data, dl_data)
    plt.show()


if __name__ == "__main__":
    main()
