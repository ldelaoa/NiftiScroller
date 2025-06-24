import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import nibabel as nib

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
            return data[:, :, self.slice_index]
        elif self.view == 'coronal':
            return data[:, self.slice_index, :]
        elif self.view == 'sagittal':
            return data[self.slice_index, :, :]

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
        self.ax.axis('off')
        plt.draw()

    def on_scroll(self, event):
        max_index = {
            'axial': self.ct_data.shape[2],
            'coronal': self.ct_data.shape[1],
            'sagittal': self.ct_data.shape[0]
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
            'axial': self.ct_data.shape[2] // 2,
            'coronal': self.ct_data.shape[1] // 2,
            'sagittal': self.ct_data.shape[0] // 2
        }[self.view]


# Load NIfTI files
root_folder = 'C:/Users/delaOArevaLR/OneDrive - UMCG/Scans/NBIA_4d/Nifti_Selected_DR/108_HM10395/'
ctname = 'CT_PlanCT_P4^P108^S304^I00008, Gated, 50.0%_ct.nii.gz'
GTname = 'rtstruct_Tumor_c50.nii.gz'
DLname = 'itv_RayStation.nii.gz'
ctpath = root_folder + ctname
gtpath = root_folder + GTname
dlpath = root_folder + DLname

ct_img = nib.load(ctpath)
gt_img = nib.load(gtpath)
dl_img  = nib.load(dlpath)
ct_data = ct_img.get_fdata()
gt_data = gt_img.get_fdata()
dl_data = dl_img.get_fdata()

# Launch the viewer
viewer = SliceViewer(ct_data, gt_data,dl_data)
plt.show()
