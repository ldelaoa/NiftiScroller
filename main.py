import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import SimpleITK as sitk

class SliceViewer:
    def __init__(self, ct_data, seg_data, dl_data):
        self.ct_data = ct_data
        self.seg_data = seg_data
        self.dl_data = dl_data

        self.view = 'axial'  # 'axial', 'coronal', or 'sagittal'
        self.slice_index = ct_data.shape[2] // 2

        self.GTshow_contour = True
        self.DLshow_contour = True

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
            self.ax.imshow(masked_dl, cmap='rainbow', alpha=0.5)

        self.ax.set_title(
            f'{self.view.capitalize()} Slice {self.slice_index} | GT [G]: {"On" if self.GTshow_contour else "Off"} | DL [D]: {"On" if self.DLshow_contour else "Off"}'
        )
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

if __name__ == "__main__":
    # Example usage
    root_folder = '//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/Sharing/RobinWi/PatientsToReview/4826048/'
    ctname = "CT_MaxExp_T=50%,PR=44% - 65%,AR()=30 - 81_ct_.nii.gz"
    GTname = 'RTstructSelected_MaxExp__GTVklieren.nii.gz'
    DLname = 'GTV50_DLContour.nii.gz'
    ctpath = root_folder + ctname
    gtpath = root_folder + GTname
    dlpath = root_folder + DLname

    ct_data = sitk.GetArrayFromImage(sitk.ReadImage(ctpath))
    gt_data = sitk.GetArrayFromImage(sitk.ReadImage(gtpath))
    dl_data  = sitk.GetArrayFromImage(sitk.ReadImage(dlpath))
    ct_data = normalize_image(ct_data, vmin=-1024, vmax=600)


    # Launch the viewer
    viewer = SliceViewer(ct_data, gt_data,dl_data)
    plt.show()
